function down_click(){
  $(".alert-success").addClass("show");
  window.setTimeout(function(){
      $(".alert-success").removeClass("show");
  },2000);
}