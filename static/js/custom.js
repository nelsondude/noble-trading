var completeTradeUrl = '/trade/complete';

function styleTradeStatus(selector) {
    $(selector).each(function() {
        var _this = $(this);
        if (_this.text().includes('accepted')) {
            _this.css('color', 'green')
        } else if (_this.text().includes('pending')) {
            _this.css('color', 'orange')
        } else if (_this.text().includes('declined')) {
            _this.css('color', 'red')
        }
    });
}

$(document).ready(function() {
    styleTradeStatus('.trade-status');
});

function completeTradeRequest(action, tradeId) {
    $.ajax({
        url: completeTradeUrl,
        method: "GET",
        data: {
            'tradeId': tradeId,
            'action': action
        },
        success: function(data) {
            window.location.href = '/';
        },
        error: function(error) {
            console.log('ERROR');
        }
    })
}

$(document.body).on("click", ".trade-complete", function(e) {
    e.preventDefault();
    var this_ = $(this);
    var tradeId = this_.attr('data-id');
    var action = this_.attr('data-action');
    completeTradeRequest(action, tradeId);
});