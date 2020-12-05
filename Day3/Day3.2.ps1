$map = Get-Content -Path ".\Day3\input.txt"
$product = 0
$position = @(0,0) #(x,y)
$tree = '#'
$numlines = $map.Count
$width = $map[0].length
$slopes = @(
			@(1,1),
			@(3,1),
			@(5,1),
			@(7,1),
			@(1,2)
		)


##remember that map[y][x]
$i = 0
$product = 1
while($i -lt $slopes.count)
{
	$position = @(0,0)
	$sloperight = $slopes[$i][0]
	$slopedown = $slopes[$i][1]
	$numtrees = 0


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
	$product *= $numtrees
	$i++
}
Write-Output $product
