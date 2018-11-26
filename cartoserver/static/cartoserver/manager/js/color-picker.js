 (function($) {
  $.fn.colorPicker = function(options) {

    var element = $(this);
    
    if (element.data('picker-id')) return;

    element.data('picker-id', getId())
    var colors = [
    '1ABC9C', '2ECC71', '3498DB', '9B59B6', '000000', 
    '16A085', '27AE60', '2980B9', '8E44AD', '2C3E50', 
    'F1C40F', 'E67E22', 'E74C3C', 'ECF0F1', '95A5A6', 
    'F39C12', 'D35400', 'C0392B', 'BDC3C7', '7F8C8D'];
    
    var invalidColorMsg = $('<span>').hide();
    invalidColorMsg.insertAfter(element);
    invalidColorMsg.css("color",'#FF0000')
    invalidColorMsg.text("Invalid color value");

    function updateElement(){
      var color = element.val();
      if(color != ''){
        if (!isColor(color)) {
          invalidColorMsg.show();
          return
        }
        invalidColorMsg.hide();
        element.css({ 
          'background-color': color,
          'color':invertColor(color)
         });
      }
      else{
        element.css({ 
          'background-color': "#FFFFFF",
          'color':"#000000"
         });
      }
    }
    element.on('change',updateElement)

    var container = $('<div>').insertAfter(element);
    container.css({
      "position":"relative"
    })
    var chooser = $('<div>').insertAfter(container).hide().data("picker-id",getId())
    chooser.css({
      "position":"absolute",
      "width":"90px",
      // "height":"120px",
      "background-color":"#FFFFFF",
      "z-index":"9999"
    })
    $.each(colors,function(index,code){
      var colorCt = $('<div>').appendTo(chooser).addClass('color-cell').data('color',"#" + code);
      colorCt.css({
        width:'16px',
        height:'16px',
        float:'left',
        'background-color': "#" + code,
        'margin':'1px',
        'cursor':'pointer'
      })
    });
    element.on('focus',function(){
      chooser.show();
      $('html').bind("click.colorPicker", function(e) {
          
          
          var target = $(e.target);
          if(target.data('picker-id') == element.data("picker-id")) return;
          chooser.hide();
          $('html').unbind("click.colorPicker");
          
          if (target.hasClass('color-cell') && target.parent().data("picker-id") == chooser.data("picker-id")) {
            element.val(target.data('color'));
            updateElement()
          }
          // Execute onClose callback whenever the color chooser is closed.
          if (options.onClose) {
            options.onClose(element);
          }
        });
    })
    updateElement()
    return this;
  };
  var counter = 0;
  function getId(){
    return "color-picker-" + (counter++);
  }
  function invertColor(hexTripletColor) {
    var color = hexTripletColor;
    color = color.substring(1);           // remove #
    color = parseInt(color, 16);          // convert to integer
    if(color > 0x888888) return "#000000"
    return "#FFFFFF"  
  }
  function isColor(val){
    return /^#[0-9A-F]{6}$/i.test(val)
  }

})(django.jQuery);
