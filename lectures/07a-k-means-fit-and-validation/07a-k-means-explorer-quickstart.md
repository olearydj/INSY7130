# K-Means Explorer: Quick Start

This optional interactive notebook lets you change the number of clusters, the distance scale, the number of starts, and the random seed while watching the fitted regions and scores change.

1. Download [07a-k-means-explorer.py](07a-k-means-explorer.py) and save it on your computer.
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you do not already have it. On macOS or Linux, run this in a terminal:

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   On Windows, run this in PowerShell:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. Open a terminal or PowerShell in the folder containing the downloaded file and run:

   ```sh
   uvx marimo run --sandbox 07a-k-means-explorer.py
   ```

The first run downloads the needed Python packages. The notebook then opens in your browser. Press Ctrl+C in the terminal when you are done.
