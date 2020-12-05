#import as raw and then split by blank lines (double newline)
$batchfile = Get-Content -Path ".\Day4\input.txt" -Raw
$batchfile = $batchfile -split "\n\n"
$numvalid = 0
$pattern = "iyr:(?:20(?:1[0-9]|20))\b|byr:(?:19[2-9]\d|200[0-2])\b|eyr:20(?:2[0-9]|30)\b|hgt:(?:(?:59|6[0-9]|7[0-6])in\b|1(?:[5-8][0-9]|9[0-3])cm)\b|hcl:#[0-9a-f]{6}\b|pid:[0-9]{9}\b|ecl:(?:amb|blu|brn|gry|grn|hzl|oth)"

#this script assumes none of them ever repeat
foreach ($i in $batchfile)
{
	#split by either a newline or a space
	$thematches = ($i -split "\n|\s") -match $pattern
	if($thematches.count -eq 7)
	{
		$numvalid++
	}
}

Write-Output $numvalid