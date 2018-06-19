(function() {
  var $, FutureMessage, spinner_template,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  $ = jQuery;

  spinner_template = '<div class="messenger-spinner">\n    <span class="messenger-spinner-side messenger-spinner-side-left">\n        <span class="messenger-spinner-fill"></span>\n    </span>\n    <span class="messenger-spinner-side messenger-spinner-side-right">\n        <span class="messenger-spinner-fill"></span>\n    </span>\n</div>';

  FutureMessage = (function(_super) {

    __extends(FutureMessage, _super);

    function FutureMessage() {
      return FutureMessage.__super__.constructor.apply(this, arguments);
    }

    FutureMessage.prototype.template = function(opts) {
      var $message;
      $message = FutureMessage.__super__.template.apply(this, arguments);
      $message.append($(spinner_template));
      return $message;
    };

    return FutureMessage;

  })(window.Messenger.Message);

  window.Messenger.themes.future = {
    Message: FutureMessage
  };

}).call(this);
