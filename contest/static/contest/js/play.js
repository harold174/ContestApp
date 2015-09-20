/**
 * Created by root on 19/09/15.
 */
$( document ).ready(function() {
    resize_videos()
});

$(".video_original").click(function(){
      var url = $(this).attr("data-url")
      var owner = $(this).attr("data-own")
      var desc = $(this).attr("data-desc")
      var playerInstance = jwplayer("original");
      playerInstance.setup({
          file: "/contest/media/"+url,
          title: 'Video of '+owner,
          description: desc
      });
      resize_videos()
});

var resize_videos = function(){
    $('.jw-skin-stormtrooper').css("width", "100%")
    $('.jw-skin-stormtrooper').css("height", "250px")
}
