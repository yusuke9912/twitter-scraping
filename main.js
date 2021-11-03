$(function(){
    $("#scrape").on("click", function(event){
      let keyword = $("#main").val();
      let scroll_count = $("#scroll_count").val();
      
      //スクレイピング結果を取得
      $.ajax({
        type: "POST",
        url: "scraping/scraping.php",
        data: { "keyword" : keyword,
                "scroll_count" : scroll_count,
          
        },
        dataType : "json",
        //リクエストが完了するまで実行される
          beforeSend: function(){
            $('.loader_wrapper').removeClass('hide');
          }
      },).done(function(scraping_data){
              //分析結果を取得
      $.ajax({
        url: 'mining/mining.php',
        type: 'post',
        data: '送信メッセージ'
    }).done(function(analyse_data){
                $('.loader_wrapper').addClass('hide');   
        $("#scraping_return_wrapper").html(`
        <table id="scraping_return" class="table table-striped" border="1">${scraping_data.text}</table>
        `);
        
        $('#tweet').removeClass('d-none');
        $('#word').removeClass('d-none');
        $('#tweet_origin').html(`<a href="https://twitter.com/search?q=${scraping_data.keyword}&src=typed_query&f=live" target="_blank" class="btn btn-link">スクレイピング元ページ</a>`)
        $('#analyse_return_wrapper').html(`
        <table id="analyse_return" class="table table-striped" border="1">${analyse_data.text}</table>
        `);
    }).fail(function(){
        console.log('analyse failed');
    });
      }).fail(function(XMLHttpRequest, status, e){
        console.log(e);
        $('.loader_wrapper').addClass('hide');
      });
      
    });
    
    
    $("#word").on("click", function(event){
      $('#analyse_return_wrapper').removeClass('d-none');
      $('#scraping_return_wrapper').addClass('d-none');
    })
    
        $("#tweet").on("click", function(event){
      $('#analyse_return_wrapper').addClass('d-none');
      $('#scraping_return_wrapper').removeClass('d-none');
    })
  });