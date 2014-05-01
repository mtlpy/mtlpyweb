/**
 * Adds a fancy marked-down box next to each post textfield for a live preview.
 **/

function ContentArea(area) {
    this.area = django.jQuery(area);

    this.previewId = function() {
        return "preview_" + this.area.attr("name");
    }

    this.createPreview = function() {
        this.area.parent().append(
            '<div style="display: inline-block; width: 400px;" id="' + this.previewId() + '_wrapper">'
            + '<b>Preview:</b>'
            + '<div id="' + this.previewId() + '"></div></div>'
        );
    }

    this.toHTML = function() {
        var content = this.area.val();
        return markdown.toHTML(content);
    }

    this.updatePreview = function() {
        console.log(this.toHTML());
        $("#" + this.previewId()).html(this.toHTML());
    }
}


django.jQuery(function() {
    $ = django.jQuery;
    content = $('.vLargeTextField[name^="content_"]');

    content.each(
        function(i, areaDom) {
            var area = new ContentArea(areaDom);
            area.createPreview();
            area.updatePreview()
            area.area.keyup(function(evt) {
                var area = new ContentArea(evt.target);
                area.updatePreview();
            });
        }
    );
})
