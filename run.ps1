$script = {
    Write-Output "Generating..."
    python .\generate.py 50 > gen_out.txt
    Write-Output "Sorting..."
    python .\sorter.py
    Write-Output "Uploading..."

    for ($i = 1; $i -lt 8; $i++) {
        python uploader.py $i
    }
}

Measure-Command {& $script| Out-Default}

