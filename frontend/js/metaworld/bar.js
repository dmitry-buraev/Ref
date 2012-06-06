define([
        'dojo/_base/declare',
        'dijit/_WidgetBase',
        'dijit/_TemplatedMixin',
        'dijit/_WidgetsInTemplateMixin',
        'dojo/text!./templates/bar.html',
        'dijit/form/Button'
], function(declare, _WidgetBase, _TemplatedMixin,
            _WidgetsInTemplateMixin, template) {
    return declare('Bar', [
                   _WidgetBase, _TemplatedMixin,
                   _WidgetsInTemplateMixin], {

        templateString: template

    });
});
