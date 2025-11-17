from __future__ import annotations


import pathway as pw

# This module defines the core streaming pipeline that the FastAPI layer talks to.
# It uses Pathway tables and the LLM xPack to keep a live index over incoming data.

class DocumentSchema(pw.Schema):
    patient_id: pw.Column[str]
    doc_type: pw.Column[str]
    content: pw.Column[str]
    source: pw.Column[str]


def build_pipeline() -> pw.Table:
    """Build a minimal streaming pipeline for the hackathon.

    In a full build you would:
    - use pw.io connectors to stream from file system, HTTP, or message bus
    - set proper watermarking and time semantics
    - attach the LLM xPack as a retrieval index or agent
    """
    # For the hackathon we keep it very simple and rely on a folder based connector.
    docs = pw.io.jsonlines.read(
        "data/stream/patient_summary/",

        schema=DocumentSchema,
        mode="streaming",
    )
    return docs


def run():
    table = build_pipeline()
    # In a more advanced version you would attach the LLM xPack here, for example:
    # from pathway.xpacks.llm import llm_app
    # app = llm_app.RAGApp.from_table(table, text_column="content")
    #
    # For the hackathon demo, the FastAPI app can query materialized
    # views over this table, or you can expose LLM calls separately.
    pw.run()
