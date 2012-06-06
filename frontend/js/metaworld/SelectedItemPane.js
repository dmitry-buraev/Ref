define([
    'dojo/_base/array',
    'dojox/lang/functional/object',
    'dojo/_base/lang',
    'dojo/_base/declare',
    'dojo/dom-construct',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dojo/text!./templates/SelectedItemPane.html',
    'dijit/registry',
    'dijit/form/TextBox',
    'dijit/form/CheckBox'
],

function(array, obj, lang, declare, domConstruct, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,
         template, registry, TextBox, CheckBox) {

    return declare('SelectedItemPane', [
                   _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

        templateString: template,

        _setItemIdAttr: function(itemId) {
            this._set('itemId', itemId);
            this.store.get(itemId).then(
                lang.hitch(this, this.showProperties),

                function(err) {
                    console.error(err);
                }
            );
        },

        showProperties: function(item) {
            //Reqired property for every Ref
            registry.byId('id').set('value', item.id);
            registry.byId('name').set('value', item.name);
            //Property of concrete Ref (In Google Datastore saves as Generic Property)
            obj.forIn(item, lang.hitch(this, function(value, key) {
                var row = domConstruct.create('div'),
                    field;
                domConstruct.create('label', {innerHTML: key, 'for': key}, row);
                if (lang.isString(value)) {
                    field = new TextBox();
                    field.set('id', key);
                    field.set('value', value);
                    field.placeAt(row);
                } else if (typeof value == 'boolean') {
                    field = new CheckBox();
                    field.set('value', value);
                    field.placeAt(row);
                }
                domConstruct.place(row, this.containerNode);
            }));
        }
    });

});
