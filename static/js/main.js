// Main JavaScript file for Inventory Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Transaction type change handler
    var transactionTypeSelect = document.getElementById('transaction_type');
    var quantityInput = document.getElementById('quantity');
    
    if (transactionTypeSelect && quantityInput) {
        transactionTypeSelect.addEventListener('change', function() {
            var productSelect = document.getElementById('product_id');
            if (productSelect.value) {
                var selectedOption = productSelect.options[productSelect.selectedIndex];
                var stockText = selectedOption.text.match(/Current Stock: (\d+)/);
                
                if (stockText && this.value === 'out') {
                    var currentStock = parseInt(stockText[1]);
                    quantityInput.setAttribute('max', currentStock);
                    
                    if (parseInt(quantityInput.value) > currentStock) {
                        quantityInput.value = currentStock;
                    }
                } else {
                    quantityInput.removeAttribute('max');
                }
            }
        });
    }
    
    // Product select change handler for transactions
    var productSelect = document.getElementById('product_id');
    if (productSelect && transactionTypeSelect && quantityInput) {
        productSelect.addEventListener('change', function() {
            if (transactionTypeSelect.value === 'out') {
                var selectedOption = this.options[this.selectedIndex];
                var stockText = selectedOption.text.match(/Current Stock: (\d+)/);
                
                if (stockText) {
                    var currentStock = parseInt(stockText[1]);
                    quantityInput.setAttribute('max', currentStock);
                    
                    if (parseInt(quantityInput.value) > currentStock) {
                        quantityInput.value = currentStock;
                    }
                }
            }
        });
    }
    
    // Search functionality for tables
    var searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            var filter = this.value.toLowerCase();
            var table = document.querySelector('.table');
            var tr = table.getElementsByTagName('tr');
            
            for (var i = 1; i < tr.length; i++) {
                var td = tr[i].getElementsByTagName('td');
                var found = false;
                
                for (var j = 0; j < td.length; j++) {
                    if (td[j]) {
                        var txtValue = td[j].textContent || td[j].innerText;
                        if (txtValue.toLowerCase().indexOf(filter) > -1) {
                            found = true;
                            break;
                        }
                    }
                }
                
                if (found) {
                    tr[i].style.display = '';
                } else {
                    tr[i].style.display = 'none';
                }
            }
        });
    }
});
