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
    'dijit/form/CheckBox',
    'dojox/grid/DataGrid',
    'dojo/store/Memory',
    'dojo/data/ObjectStore'
],

function(array, obj, lang, declare, domConstruct, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,
         template, registry, TextBox, CheckBox, DataGrid, Memory, ObjectStore) {

    return declare('SelectedItemPane', [
                   _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

        baseClass: 'selected-item-pane',

        templateString: template,

        _setItemIdAttr: function(itemId) {
            this._set('itemId', itemId);
            this.store.get(itemId).then(
                lang.hitch(this, this.renderItem),

                function(err) {
                    console.error(err);
                }
            );
        },

        renderItem: function(item) {
            //Reqired property for every Ref
            registry.byId('id').set('value', item.id);
            registry.byId('name').set('value', item.name);
            domConstruct.empty(this.selfPropertiesNode); //Remove properties from previouse selected Ref
            var propsGird = registry.byId('props-grid');
            if (propsGird) {
                propsGird.destroy();
            }
            if (item.is_group) {
                this.renderGroupRef(item);
            }
        },

        renderGroupRef: function(ref) {
            //Render properties of concrete Ref (In Google Datastore saves as Generic Property)
            obj.forIn(ref, lang.hitch(this, function(value, key) {
                if (array.indexOf(
                        ['id', 'name', 'level', 'is_group', 'children', 'el_props'], key) === -1) {
                    var row = domConstruct.create('div', {'class': 'row'}),
                        field;
                    domConstruct.create('label', {innerHTML: key, 'for': key}, row);
                        field = new TextBox();
                        field.set('id', key);
                        field.set('value', value);
                        field.placeAt(row);
                    domConstruct.place(row, this.selfPropertiesNode);
                }
            }));
            //Render grid needed to add, edit and delete attributes of Ref elements
            var attributesStore = new Memory({data: ref.el_props, idProperty: 'name'}),
                grid = new DataGrid({
                    store: ObjectStore({objectStore: attributesStore}),
                    defaultCell: '100px',
                    rowSelector: '20px',
                    autoWidth: true,
                    autoHeight: true,
                    structure: [
                        {name: 'name', field: 'name', width: '160px', editable: true},
                        { name: 'type', field: 'type', width: '150px',
                          cellType: 'dojox.grid.cells.Select',
                          options: ['bool', 'int', 'string', 'text'],
                          editable: true
                        }
                    ]
                }, this.attributesGrid);
            grid.startup();
        }
    });

});
