# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import newspaper
from newspaper import Article

from synthora.toolkits.base import BaseToolkit
from synthora.toolkits.decorators import tool
from synthora.types.enums import Ok, Result


class NewsToolkit(BaseToolkit):
    def __init__(self, memoize_articles: bool = True):
        super().__init__()
        self.memoize_articles = memoize_articles

    @tool
    def get_article_list(
        self, base_url: str, num_articles: int = 20
    ) -> Result[str, Exception]:
        """
        Get a list of articles from a news website.

        Args:
            base_url: The base URL of the news website. eg, https://cnn.com
            num_articles: The number of articles to get.

        Returns:
            Result: A list of article URLs.
        """
        articles = newspaper.build(
            base_url, memoize_articles=self.memoize_articles
        ).articles[:num_articles]
        return Ok([article.url for article in articles])

    @tool
    def get_full_text_by_url(self, url: str) -> Result[str, Exception]:
        """
        Get the full text of an article from a URL.

        Args:
            url: The URL of the article.

        Returns:
            Result: The full text of the article.
        """
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return Ok(
            f"""
            Title: {article.title}
            Authors: {article.authors}
            Publish Date: {article.publish_date}
            Text: {article.text}
            """
        )

    def get_summary_by_url(self, url: str) -> Result[str, Exception]:
        r"""
        Get the summary of an article from a URL.

        Args:
            url: The URL of the article.

        Returns:
            Result: The summary of the article.
        """
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return Ok(
            f"""
            Title: {article.title}
            Authors: {article.authors}
            Publish Date: {article.publish_date}
            Summary: {article.summary}
            """
        )
