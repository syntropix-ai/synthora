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

.PHONY: all format help docs

# Default target executed when no arguments are given to make.
all: help

# Define a variable for the test file path.
TEST_FILE ?= tests/unit/

clean:
	cd docs && make clean

docs:
	make html
	poetry run python -m http.server -d docs/build/html 8000

test:
	poetry run pytest $(TEST_FILE)

install:
	poetry install --with quality,dev
	poetry run pre-commit install

format:
	poetry run pre-commit run --all-files

publish:
	poetry build && poetry publish --build


# Documentation

html:
	cd docs && sphinx-apidoc -o source ../src/ && make html

help:
	@echo '===================='
	@echo '-- DOCUMENTATION ---'
	@echo '--------------------'
	@echo 'install                      - install dependencies'
	@echo 'format                       - run code formatters'
	@echo 'test                         - run unit tests'
