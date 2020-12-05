#import as raw and then split by blank lines (double newline)
$batchfile = Get-Content -Path ".\Day4\input.txt" -Raw
$batchfile = $batchfile -split "\n\n"
$numvalid = 0

#this script assumes none of them ever repeat
foreach ($i in $batchfile)
{
	#split by either a newline or a space
	if((($i -split "\n|\s") -match "(byr|iyr|eyr|hgt|hcl|ecl|pid)").count -eq 7)
	{
		$numvalid++
	}
}

Write-Output $numvalid