import logging
from typing import Any, List, Optional, Type

from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.schema import BaseNode, MetadataMode
from llama_index.core.vector_stores.types import (
    BasePydanticVectorStore,
    VectorStoreQuery,
    VectorStoreQueryResult,
)
from llama_index.core.vector_stores.utils import metadata_dict_to_node, node_to_metadata_dict


_logger = logging.getLogger(__name__)


def get_data_model(
    base: Type,
    index_name: str,
    schema_name: str,
    embed_dim: int = 1536,
    native_vector: bool = False,
) -> Any:
    """
    This part create a dynamic sqlalchemy model with a new table.
    """
    from sqlalchemy import Column
    from sqlalchemy.types import BIGINT, TEXT, VARCHAR
    from sqlalchemy_iris import IRISListBuild
    from sqlalchemy_iris import IRISVector

    tablename = "data_%s" % index_name
    class_name = "Data%s" % index_name

    class AbstractData(base):  # type: ignore
        __abstract__ = True  # this line is necessary
        id = Column(BIGINT, primary_key=True, autoincrement=True)
        text = Column(TEXT, nullable=False)
        metadata_ = Column(TEXT)
        node_id = Column(VARCHAR(200))
        partition_id = Column(VARCHAR(200))
        embedding = Column(IRISVector(embed_dim) if native_vector else IRISListBuild(embed_dim))  # type: ignore

    return type(
        class_name,
        (AbstractData,),
        {"__tablename__": tablename, "__table_args__": {"schema": schema_name}},
    )


class IRISVectorStore(BasePydanticVectorStore):
    from sqlalchemy.sql.selectable import Select

    stores_text = True
    flat_metadata = True

    connection_string: str
    table_name: str
    schema_name: str
    embed_dim: int
    perform_setup: bool
    debug: bool

    _base: Any = PrivateAttr()
    _table_class: Any = PrivateAttr()
    _engine: Any = PrivateAttr()
    _session: Any = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)
    _native_vector: bool = PrivateAttr(default=False)

    def __init__(
        self,
        connection_string: str,
        table_name: str,
        schema_name: str,
        embed_dim: int = 1536,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> None:
        table_name = table_name.lower()
        schema_name = schema_name.lower()

        super().__init__(
            connection_string=connection_string,
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            perform_setup=perform_setup,
            debug=debug,
        )

    async def close(self) -> None:
        if not self._is_initialized:
            return

        self._session.close_all()
        self._engine.dispose()

    @classmethod
    def class_name(cls) -> str:
        return "IRISVectorStore"

    @classmethod
    def from_params(
        cls,
        hostname: Optional[str] = None,
        port: Optional[str] = None,
        namespace: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "llamaindex",
        schema_name: str = "SQLUser",
        connection_string: Optional[str] = None,
        embed_dim: int = 1536,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "IRISVectorStore":
        """Return connection string from database parameters."""
        conn_str = (
            connection_string
            or f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
        )
        return cls(
            connection_string=conn_str,
            table_name=table_name,
            schema_name=schema_name,
            embed_dim=embed_dim,
            perform_setup=perform_setup,
            debug=debug,
        )

    @property
    def client(self) -> Any:
        if not self._is_initialized:
            return None
        return self._engine

    def _connect(self) -> Any:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        self._engine = create_engine(self.connection_string, echo=self.debug)
        self._session = sessionmaker(self._engine)
        with self._engine.connect() as conn:
            self._native_vector = conn.dialect.supports_vectors

            from sqlalchemy.orm import declarative_base

            # sqlalchemy model
            self._base = declarative_base()
            self._table_class = get_data_model(
                self._base,
                self.table_name,
                self.schema_name,
                embed_dim=self.embed_dim,
                native_vector=self._native_vector,
            )

    def _create_tables_if_not_exists(self) -> None:
        with self._session() as session, session.begin():
            self._base.metadata.create_all(session.connection())

    def _create_vector_functions(self) -> None:
        if self._native_vector:
            return
        try:
            from sqlalchemy import text

            with self._session() as session, session.begin():
                session.execute(
                    text(
                        """
CREATE OR REPLACE FUNCTION llamaindex_l2_distance(v1 VARBINARY, v2 VARBINARY)
RETURNS NUMERIC(0,16)
LANGUAGE OBJECTSCRIPT
{
    set dims = $listlength(v1)
    set distance = 0
    for i=1:1:dims {
        set diff = $list(v1, i) - $list(v2, i)
        set distance = distance + (diff * diff)
    }

    quit $zsqr(distance)
}
"""
                    )
                )
                session.execute(
                    text(
                        """
CREATE OR REPLACE FUNCTION llamaindex_cosine_distance(v1 VARBINARY, v2 VARBINARY)
RETURNS NUMERIC(0,16)
LANGUAGE OBJECTSCRIPT
{
    set dims = $listlength(v1)
    set (distance, norm1, norm2, similarity) = 0

    for i=1:1:dims {
        set val1 = $list(v1, i)
        set val2 = $list(v2, i)

        set distance = distance + (val1 * val2)
        set norm1 = norm1 + (val1 * val1)
        set norm2 = norm2 + (val2 * val2)
    }

    set similarity = distance / $zsqr(norm1 * norm2)
    set similarity = $select(similarity > 1: 1, similarity < -1: -1, 1: similarity)
    quit 1 - similarity
}
"""
                    )
                )
                session.execute(
                    text(
                        """
CREATE OR REPLACE FUNCTION llamaindex_inner_distance(v1 VARBINARY, v2 VARBINARY)
RETURNS NUMERIC(0,16)
LANGUAGE OBJECTSCRIPT
{
    set dims = $listlength(v1)
    set distance = 0

    for i=1:1:dims {
        set val1 = $list(v1, i)
        set val2 = $list(v2, i)

        set distance = distance + (val1 * val2)
    }

    quit distance
}
"""
                    )
                )
                session.commit()
        except Exception as e:
            raise Exception(f"Failed to create vector functions: {e}") from e

    def _initialize(self) -> None:
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                self._create_vector_functions()
                self._create_tables_if_not_exists()
            self._is_initialized = True

    def _node_to_table_row(self, node: BaseNode) -> Any:
        import json

        return self._table_class(
            node_id=node.node_id,
            embedding=node.get_embedding(),
            text=node.get_content(metadata_mode=MetadataMode.NONE),
            partition_id=node.ref_doc_id,
            metadata_=json.dumps(
                node_to_metadata_dict(
                    node,
                    remove_text=True,
                    flat_metadata=self.flat_metadata,
                )
            ),
        )

    def add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        self._initialize()
        ids = []
        with self._session() as session, session.begin():
            for node in nodes:
                ids.append(node.node_id)
                item = self._node_to_table_row(node)
                session.add(item)
            session.commit()
        return ids

    def delete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        from sqlalchemy import delete

        self._initialize()
        with self._session() as session, session.begin():
            stmt = delete(self._table_class).where(
                self._table_class.partition_id == ref_doc_id
            )

            session.execute(stmt)
            session.commit()

    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        import json

        from sqlalchemy import select, text

        self._initialize()
        query_embedding = [float(v) for v in query.query_embedding]

        rows = []
        with self._session() as session, session.begin():
            stmt = (
                select(  # type: ignore
                    self._table_class.id,
                    self._table_class.node_id,
                    self._table_class.text,
                    self._table_class.metadata_.label("metadata"),
                    (
                        self._table_class.embedding.cosine(query_embedding).label(
                            "distance"
                        )
                        if self._native_vector
                        else self._table_class.embedding.func(
                            "llamaindex_cosine_distance", query_embedding
                        ).label("distance")
                    ),
                )
                .limit(query.similarity_top_k)
                .order_by(text("distance asc"))
            )
            rows = session.execute(
                stmt,
            )

        nodes = []
        similarities = []
        ids = []
        for row in rows:
            node = metadata_dict_to_node(json.loads(row.metadata))
            node.set_content(str(row.text))
            similarities.append(
                (1 - float(row.distance)) if row.distance is not None else 0
            )
            ids.append(row.node_id)
            nodes.append(node)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )