document.addEventListener("DOMContentLoaded", function () { 
  $(function () {
      $('a[href^=#]').click(function() {
      var speed = 500; // スクロール速度(ミリ秒)
      var href = $(this).attr("href");
      var target = $(href == "#" || href == "" ? 'html' : href);
      var position = target.offset().top;
      $('html').animate({scrollTop:position}, speed, 'swing');
      return false;
      });
      });

      $('input[type=checkbox]').change(function(){
          counter = 0;
          clicked = $(this).data('index');
          $('input[type=checkbox]').each(function(){
            if($(this)[0].checked){
              counter++;
            }
          });
          if(counter==3){    
            toDisable = clicked;
            while(toDisable==clicked){
              toDisable=Math.round(Math.random()*2);
            }
            $("input:eq("+toDisable+")")[0].checked = false;
          }
      });
  })