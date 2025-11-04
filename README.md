# Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Use of `eval`** | Security | 59 | `eval("...")` can execute arbitrary code (Bandit B307). This is a major security vulnerability. | Removing the `eval` call. |
| **Mutable Default Argument** | Bug | 8 | `logs=[]` is a mutable default argument. This list will be shared and persist across all calls to `addItem`. | Changing the default to `logs=None` and initializing `logs = []` inside the function. |
| **Missing Input Validation** | Bug / Robustness | 8, 51 | `addItem` accepts invalid types (like 123, "ten") and negative quantities, which can corrupt the `stock_data`. | Adding type checks (`isinstance`) and value checks (`qty >= 0`) and raise a `ValueError`. |
| **Potential `KeyError`** | Bug | 23 | `getQty` directly accesses `stock_data[item]`, which will crash if the item doesn't exist. | Use of `stock_data.get(item, 0)` to safely return 0 for missing items. |
| **Bare `except`** | Reliability | 19-20 | `except: pass` catches all exceptions (including `SystemExit`) and silently ignores them, hiding bugs. | Catching the *specific* exception you expect (e.g., `KeyError`). |
| **Unsafe File Handling** | Reliability | 26-34 | `open()` is used without a `with` block, risking resource leaks if an error occurs. No file encoding (`"utf-8"`) is specified. | Using the `with open(file, mode, encoding="utf-8") as f:` context manager. |
| **Global Variable** | Design | 6, 28 | The code relies on a mutable `global stock_data`. `loadData` rebinds it with the `global` keyword. This makes the code hard to test and reason about. | Passing `stock_data` as a parameter to functions that need it. Having `loadData` return the dictionary. |
| **PEP8 Naming** | Style | 8, 14, 22... | Functions use `camelCase` (e.g., `addItem`) instead of the PEP8 standard `snake_case` (e.g., `add_item`). | Renaming all functions to `snake_case`. |
| **Missing Docstrings** | Maintainability | All | No module or function docstrings exist, making the code's purpose and usage unclear. | Adding a module docstring and docstrings to all functions describing their purpose, arguments, and return values. |
| **Unused Import** | Style | 2 | `import logging` is included but the `logging` module is never used. | Removing the import (or, preferably, use it for logging errors instead of `print`). |
| **Old-Style Formatting** | Style | 12 | Uses old `%`-style string formatting, which is less readable than f-strings. | Converting `"%s: Adding %d..."` to an f-string. |


# Answers

1)The easiest problems to resolve were the quick, localized fixes. For instance, removing the eval call was a one-line deletion that instantly eliminated a serious security vulnerability. Similarly, updating stock_data[item] to stock_data.get(item, 0) in getQty neatly prevented potential crashes due to missing keys — a clean, Pythonic solution. These changes were simple because they were self-contained and didn’t affect other parts of the codebase.

The most challenging issue, however, was refactoring the code to remove the global stock_data variable. Unlike the smaller fixes, this required a broader redesign that impacted nearly every function. It involved modifying multiple function definitions to take stock_data as an argument and adjusting the main() function to manage and pass this state around. This fundamentally restructured how data flowed through the program.

2)None of the findings from the static analysis tools were false positives. Every warning raised by tools like Pylint and Bandit corresponded to a legitimate issue. The eval call posed a genuine security threat, the mutable default argument introduced subtle bugs, and the bare except was hiding potential errors. Even the stylistic flags, such as naming inconsistencies and missing docstrings, correctly identified areas that reduced readability and maintainability.

3)In a real-world workflow, I would integrate static analysis tools at two stages. First, locally during development, I’d enable Pylint or Flake8 extensions in my IDE (such as VS Code) to get immediate feedback while writing code. I’d also set up pre-commit hooks to run basic linting on staged files before every commit. Second, in the CI/CD pipeline, I’d add a dedicated Static Analysis step that runs on every pull request. This would automatically block merges if any critical issues were detected, ensuring high-quality, secure code in the main branch.

4)The overall quality of the code improved dramatically after applying the fixes. The most notable improvement was in reliability and resilience. The program can now handle missing items and file-related errors gracefully instead of crashing. Input validation ensures that only correct data is processed, while secure coding practices eliminate dangerous vulnerabilities like eval. The design is also cleaner — removing the global variable makes the flow of data explicit and predictable. Combined with proper naming conventions and added documentation, the code is now much easier to read, maintain, and extend.
