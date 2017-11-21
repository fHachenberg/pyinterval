function instrumented_make() {    
    pyinterval_instrument "make $*"
    return $?
}
# Instrumentierung zum Loggen von unproduktiven Zeiten
alias make=instrumented_make
