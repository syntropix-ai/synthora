<!-- LICENSE HEADER MANAGED BY add-license-header

Copyright 2024-2025 Syntropix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Installation Guide

## Install from PyPI (Recommended)

For most users, installing Synthora from PyPI is the simplest and most recommended approach. You can get started with just one command:

```shell
pip install synthora
```

This will install the core components of `synthora`.

### Optional Add-ons:
- **Pre-built Toolkits**:
  To include Synthora's pre-built tools, use:
  ```shell
  pip install "synthora[toolkits]"
  ```

- **Pre-built Services**:
  For pre-configured services, use:
  ```shell
  pip install "synthora[services]"
  ```

- **All Dependencies**:
  To install all optional dependencies, use:
  ```shell
  pip install "synthora[all]"
  ```

---

## Install from Source

Installing from source is ideal for developers. It allows full customization and the freedom to modify components to meet specific needs. This aligns with Synthora's design philosophy: we aim to provide a flexible core without overloading pre-built components. By leveraging inheritance, you can easily implement your desired features (trust us, Synthora takes care of the tricky parts).

### Steps to Install from Source:

#### Install with `poetry` (Recommended):

1. Clone the GitHub repository:
   ```shell
   git clone https://github.com/syntropix-ai/synthora.git
   ```

2. Navigate to the project directory:
   ```shell
   cd synthora
   ```

3. Install Poetry (if not already installed):
   ```shell
   pip install poetry
   ```

4. Activate the Poetry environment:
   ```shell
   poetry shell
   ```

5. Install the core components:
   ```shell
   poetry install
   ```

6. **Alternatively**, install all optional components:
   ```shell
   poetry install -E all
   ```

---

### Install with `pip`

If you prefer to install Synthora in an editable mode for development purposes, you can use the following method:

1. Clone the repository (if not done already):
   ```shell
   git clone https://github.com/syntropix-ai/synthora.git
   ```

2. Navigate to the project directory:
   ```shell
   cd synthora
   ```

3. Use `pip` to install in editable mode:
   ```shell
   pip install -e .
   ```

4. **Optional**: If you need all optional dependencies, use:
   ```shell
   pip install -e .[all]
   ```

This method is particularly useful if you plan to make changes to Synthora's codebase, as it reflects changes instantly without the need for reinstallation.
