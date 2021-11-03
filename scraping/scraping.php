<?php
$keyword = $_POST['keyword'];
$scroll_count = $_POST['scroll_count'];

$command="python scraping.py ".$keyword." ".$scroll_count;
exec($command,$outputs);

$text = "
<thead>
  <tr>
    <th>No</th>
    <th>ユーザー名</th>
    <th>日付</th>
    <th>ツイート</th>
  </tr>
</thead>
";
foreach($outputs as $output){
    $text .= $output."\n";
}

  $list = array("text" => $text, "keyword" => $keyword);
  header("Content-type: application/json; charset=UTF-8");
  echo json_encode($list,JSON_UNESCAPED_UNICODE);
  exit;

?>