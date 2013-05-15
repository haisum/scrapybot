<?php
$json = file_get_contents($argv[1]);//or whatever file contains json
$episodes = json_decode($json,true);
function parseJsonToSql($json, $tableKey, $htmlFormatted = false){
	$createStatements = "";
	$strings = array();
	foreach ($json as $key => $value) {
		if(is_array($value)){
			$createStatements .= parseJsonToSql($value, $tableKey, $htmlFormatted);
		}
		else{
			$strings[$key] = $value;
		}
	}
	if(!empty($strings)){
		$values = array_map("filterForSql", $strings);
		$keys = array_keys($strings);
		$createStatements .= "INSERT INTO `{$strings[$tableKey]}` (`" . implode("`,`", $keys) ."`) VALUES(\"" . implode("\",\"", $values) . "\");";
	}
	if($htmlFormatted){
		return "<pre>" . $createStatements . "</pre><br/>";
	}
	else{
		return $createStatements;
	}
}
function filterForSql($input){
	return addslashes($input);
}
echo parseJsonToSql($episodes, "itemName");
?>
