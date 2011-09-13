/**
 *   Simple framework for data tables.
 */

function DataTable(options) {
    var selectedRow = null;

    this.options = options;
    this.data = {};

    this.updateData = function(sync) {
        var _this = this;
        $.ajax({ type: 'GET'
               , async: (sync == undefined ? false : !sync)
               , url: this.options.dataUrl
               , data: this.options.dataUrlParams
               , dataType: 'json'
               , success: function(res) { _this.requestSuccess(res); }
               });
    }

    this.requestSuccess = function(res) {
        if( res.success ) {
            this.data = res.records;
        } else {
            if( this.options.error )
                this.options.error('Errore nel recupero dati: '+res.message);
        }
        
        if( this.options.onUpdate != null )
            this.options.onUpdate(res.success, res.records);
    }

    this.update = function(update_data) {
        if( update_data == true ) this.updateData(true);
        this.table.find('tbody').empty();
        for(i in this.data) {
            this.addRow(this.data[i]);
        }
    }

    this.addRow = function(rowData) {
        var _this = this;
        var tbody = this.table.find("tbody");
        var tr = $(document.createElement('tr'))
                    .attr('id', rowData.id)
                    .click(function() { _this.selectRow(this.id); });
        for(j in this.options.columns) {
            var column = this.options.columns[j];
            $(document.createElement('td'))
                .attr('id', column.field)
                .addClass('data')
                .html(rowData[column.field])
                .appendTo(tr);
        }
        tr.appendTo(tbody);
    }

    this.deleteRow = function(rowId) {
        this.table.find("tbody tr#"+rowId).remove();
    }

    this.selectRow = function(id) {
        selectedRow = id;
        this.table.find("tbody tr").removeClass('selected');
        this.table.find("tbody tr#"+id).addClass('selected');
        if( this.options.onRowSelect != null )
            this.options.onRowSelect(selectedRow);
    }

    this.getSelectedRow = function(message) {
        return selectedRow;
    }

    this.getRowData = function(rowId) {
        var data = {};
        var row = this.table.find("tbody tr#"+rowId);
        if( row == null ) return null;
        row.find('td.data').each(function(i, element) {
            data[element.id] = element.innerHTML;
        });
        return data;
    }

    this.setRowData = function(rowId, data) {
        var row = this.table.find("tbody tr#"+rowId);
        this.data[rowId] = data;
        if( row == null ) return null;
        row.find('td.data').each(function(i, element) {
            $(element).html(data[element.id]);
        });
    }

    this.sortBy = function(field, direction) {
        var i = (direction == 'asc' ? -1 : +1);
        this.data = this.data.sort(function(a, b) {
            return i*( a[field] - b[field] );
        });
        this.update(false);
    }

    // ---- init ----

    // -- create table
    this.table = $(document.createElement('table'));

    var thead = $(document.createElement('thead'));
    for(i in this.options.columns) {
        var column = this.options.columns[i];
        $(document.createElement('th'))
            .html(column.name)
            .appendTo(thead);
    }
    thead.appendTo(this.table);

    $(document.createElement('tbody')).appendTo(this.table);
    this.update(true);

    // -- pack
    $(this.options.element).append(this.table);
}



