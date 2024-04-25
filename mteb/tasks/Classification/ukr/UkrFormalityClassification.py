from __future__ import annotations

from mteb.abstasks import AbsTaskClassification
from mteb.abstasks.TaskMetadata import TaskMetadata


class UkrFormalityClassification(AbsTaskClassification):
    metadata = TaskMetadata(
        name="UkrFormalityClassification",
        description="""
        This dataset contains Ukrainian Formality Classification dataset obtained by
        trainslating English GYAFC data.
        English data source: https://aclanthology.org/N18-1012/
        Translation into Ukrainian language using model: https://huggingface.co/facebook/nllb-200-distilled-600M
        Additionally, the dataset was balanced, witha labels: 0 - informal, 1 - formal.
        """,
        dataset={
            "path": "ukr-detect/ukr-formality-dataset-translated-gyafc",
            "revision": "671d1e6bbf45a74ef21af351fd4ef7b32b7856f8",
        },
        reference="https://huggingface.co/datasets/ukr-detect/ukr-formality-dataset-translated-gyafc",
        type="Classification",
        category="s2s",
        eval_splits=["test"],
        eval_langs=["ukr-Cyrl"],
        main_score="accuracy",
        date=("2018-04-11", "2018-06-20"),
        form=["written"],
        domains=["News"],
        task_subtypes=["Topic classification"],
        license="openrail++",
        socioeconomic_status="mixed",
        annotations_creators="derived",
        dialect=[],
        text_creation="machine-translated",
        bibtex_citation="""@inproceedings{rao-tetreault-2018-dear,
        title = "Dear Sir or Madam, May {I} Introduce the {GYAFC} Dataset: Corpus, Benchmarks and Metrics for Formality Style Transfer",
        author = "Rao, Sudha  and
        Tetreault, Joel",
        booktitle = "Proceedings of the 2018 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers)",
        month = jun,
        year = "2018",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/N18-1012",
        }""",
        n_samples={"test": 4853},
        avg_character_length={"test": 52.39},
    )

    def dataset_transform(self):
        self.dataset = self.dataset.rename_column("labels", "label")
        self.dataset = self.dataset.class_encode_column("label")
        self.dataset = self.dataset["test"].train_test_split(
            test_size=0.5, seed=self.seed, stratify_by_column="label"
        )  # balanced sampling


if __name__ == "__main__":
    from sentence_transformers import SentenceTransformer

    from mteb import MTEB

    # intfloat/multilingual-e5-small
    model_name = "intfloat/multilingual-e5-small"
    model = SentenceTransformer(model_name)
    evaluation = MTEB(tasks=[UkrFormalityClassification()])
    evaluation.run(model)
