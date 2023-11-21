from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp

from base.config import Config


class Generator(Config):
    """Generator, aka LLM, to provide an answer based on some question and context"""

    def __init__(self, template) -> None:
        super().__init__()
        # load Llama from local file
        self.llm = LlamaCpp(
            model_path=f"{self.parent_path}/{self.config['generator']['llm_path']}",
            n_ctx=self.config["generator"]["context_length"],
        )
        # create prompt template
        self.prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

    def get_answer(self, context: str, question: str) -> str:
        """
        Get the answer from llm based on context and user's question
        Args:
            context (str): most similar document retrieved
            question (str): user's question
        Returns:
            str: llm answer
        """

        query_llm = LLMChain(
            llm=self.llm, prompt=self.prompt, llm_kwargs={"max_tokens": 5000}
        )

        return query_llm.run({"context": context, "question": question})
