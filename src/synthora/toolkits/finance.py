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


import yfinance as yf

from synthora.toolkits.base import BaseToolkit
from synthora.toolkits.decorators import tool
from synthora.types.enums import Ok, Result


class FinanceToolkit(BaseToolkit):
    @tool
    @staticmethod
    def get_stock_price(symbol: str) -> Result[str, Exception]:
        """
        Get the stock price of a company by symbol.

        Args:
            symbol: The stock symbol.

        Returns:
            Result: The stock price.
        """
        stock = yf.Ticker(symbol)
        return Ok(stock.history(period="7d").to_json())

    @tool
    @staticmethod
    def get_company_news_urls(symbol: str) -> Result[str, Exception]:
        """
        Get the latest news urls about a company by symbol.

        Args:
            symbol: The stock symbol.

        Returns:
            Result: The latest news.
        """
        stock = yf.Ticker(symbol)
        results = []
        for news in stock.news:
            try:
                results.append(
                    {
                        "url": news["content"]["clickThroughUrl"]["url"],
                        "title": news["content"]["title"],
                        "summary": news["content"]["summary"],
                    }
                )
            except Exception:
                pass
        return Ok(results)
