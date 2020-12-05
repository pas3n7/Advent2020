$map = Get-Content -Path ".\Day3\input.txt"
$numtrees = 0
$sloperight = 3 #(x)
$slopedown = 1 #(y)
$position = @(0,0) #(x,y)
$tree = '#'
$numlines = $map.Count
$width = $map[0].length


##remember that map[y][x]

while (($position[1] + $slopedown) -le $numlines  )
{

	#check if we are on a tree
	if ($map[$position[1]][$position[0]] -eq $tree)
	{
		$numtrees++
	}

	#now move
	$position[0] = ($position[0] + $sloperight) % $width
	$position[1] += $slopedown
}


Write-Output $numtrees