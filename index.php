<?php
set_time_limit(0);

?>

<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>スクレイピング</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    <link rel="stylesheet" href="main.css" type="text/css" />
</head>

<body>
    <div id="container">
        <h1>ソーシャルリスニングツール</h1>

        <div class="container">
            <div class="row">
                <div class="col-4">
                    <div class="input-group mb-3">
                        <span class="input-group-text">キーワードを入力</span>
                        <input type="text" id="main" class="form-control">
                    </div>
                </div>
                <div class="col-4">
                    <div class="input-group mb-3">
                        <span class="input-group-text">スクロール回数を入力</span>
                        <input type="number" id="scroll_count" class="form-control">
                    </div>
                </div>
                <div class="col-4"><button id="scrape" class="btn btn-dark">スクレイピング</button></div>
            </div>
        </div>



        <button id="tweet" class="btn btn-outline-primary d-none">ツイート</button>
        <button id="word" class="btn btn-outline-primary d-none">頻出単語</button></p>

        <div id="tweet_origin"></div>

        <div id="result_nav">
            <div id="scraping_return_wrapper"></div>
            <div id="analyse_return_wrapper" class="d-none"></div>
        </div>

        <div class="loader_wrapper hide">
            <table class="loader"></table>
            <h2 class="loading_message">スクレイピング中</h2>
        </div>

    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW"
        crossorigin="anonymous"></script>
    <script src="./main.js"></script>
</body>

</html>