# Find Old Large Files

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Find Old Large Files is a powerful, open-source utility designed to declutter your computer by identifying and removing large, old files. It provides an open-source alternative to CleanMyMac X with comparable functionality.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Safety](#safety)
- [Contributing](#contributing)
- [License](#license)

## Features

| **Features** | **Find Old Large Files** | **CleanMyMac X** |
|:------------:|:------------------------:|:----------------:|
| Search for Large, Old Files | ✔️ | ✔️ |
| Safe Deletion | ✔️ | ✔️ |
| Exclusion List | ✔️ | ❌ |
| Free & Open Source | ✔️ | ❌ |

- **Search Large, Old Files:** Scan your desired directory for files that exceed a specified size and are older than a certain number of days.
- **Safe Deletion:** This tool doesn't delete files outright. Instead, it moves them to a designated "trash" directory, allowing you to restore them if necessary.
- **Exclusion List:** You can list file extensions to exclude from the scan. This feature ensures important file types aren't moved to the trash.
- **Free & Open Source:** Unlike CleanMyMac X, Find Old Large Files is completely free to use and open-source, promoting transparency and community involvement.

## Installation

Install Find Old Large Files with ease using pip:

```bash
pip install find_old_large_files
```

## Usage

Find Old Large Files is designed with user convenience in mind and can be used via the command line in two primary ways:

### Default Use

By default, Find Old Large Files is configured to scan your home directory. It searches for files that are larger than 100MB and older than 365 days, moving matching files to a designated 'trash' directory within your home directory. To use the utility with these default parameters, use the following command:

```bash
find_old_large_files
```

### Custom Use
If you wish to customize the utility to meet specific requirements, you can modify the parameters as follows:

```bash
python find_old_large_files.py --size 200 --days 180 --dir /Users/username/Documents --exclude .pdf .docx --trash /Users/username/trash
```

Detailed explanation of the parameters:

--size: Sets the file size limit in MB. Files larger than this limit will be moved to the trash. This allows you to manage files based on their sizes. Default value is 100MB.
--days: Specifies the file age limit in days. Files older than this limit will be moved to the trash. This is useful for managing files based on their last modified date. Default value is 365 days.
--dir: Defines the directory to scan for large, old files. This gives you control over the directories to be scanned. Default directory is the home directory.
--exclude: Allows you to provide a list of file extensions to exclude from the scan. This is crucial to prevent important file types from being moved to the trash. Default excluded extensions are '.docx' and '.xlsx'.
--trash: Determines the directory where the large, old files will be moved. This lets you manage your file deletions more effectively. Default directory is a 'trash' directory within the home directory.

### Examples

Here are some common usage scenarios:

1. To scan a specific directory for large, old files:

```bash
python find_old_large_files.py --dir /path/to/directory
```

2. To exclude certain file types from being moved to the trash:
```bash
python find_old_large_files.py --exclude .pdf .docx
```

3. To change the destination directory for files moved to trash:

```bash
python find_old_large_files.py --trash /path/to/trash
```

### Troubleshooting

In case of any errors or issues, please refer to the log file file_scanner.log in your trash directory for details. If the problem persists, feel free to open an issue on the GitHub repository.

Find Old Large Files is engineered to ensure user safety. It won't delete any files without your confirmation, and it lets you review the files marked for deletion before moving them to the trash. However, as with any utility that modifies your file system, we recommend using it with caution. Always ensure your crucial files are backed up before using Find Old Large Files.

## Contributing

We warmly welcome and appreciate contributions from the community! Whether it's a bug report, new feature, correction, or additional documentation, we thank you for helping us improve Find Old Large Files. Here's how you can contribute:

1. **Fork the Repository**: Start by forking the [Find Old Large Files](https://github.com/yourusername/find_old_large_files) repository to your own GitHub account.

2. **Clone the Repository**: Clone the forked repository to your local machine to work on.

   ```bash
   git clone https://github.com/yourusername/find_old_large_files.git
   ```

3. Create a New Branch: Make a new branch in Git to keep your changes isolated from the main branch. This allows you to submit and manage multiple contributions.
```bash
git checkout -b name_of_your_new_branch
```

4. Make Necessary Changes: Add, edit or delete whatever is necessary. Ensure your changes align with the project's coding style and standards.

5. Commit Changes: After making the changes, commit them with a concise and descriptive commit message.

```bash
git commit -m "A brief description of the change"
```

6. Push Changes: Push your changes to your forked repository.

```bash
git push origin name_of_your_new_branch
```

Submit a Pull Request: Go to the Find Old Large Files repository, and you'll see your recently pushed branch. Click on 'Compare & pull request' and submit your pull request with a brief description of your changes.

If you have any questions or need assistance, please open an issue, and we'd be glad to help!

Remember to replace `yourusername` with your actual GitHub username. This updated section should make the contributing process clearer and more engaging for potential contributors.


## License

Find Old Large Files is licensed under the terms of the MIT license. See LICENSE for the full text.