package alfio.util;

public class choosingCurrencyFactory {
    public choosingCurrencyFactory(){}
    public static Currency get(choosingCurrencyID strategyID) {
        Currency currency = null;
        switch(strategyID) {
            case UNITED_STATES:
                currency = new USAcurrency();
                break;
            case CANADA:
                currency = new CANADAcurrency();
                break;
            case ITALY:
                currency = new ITALYcurrency();
                break;
            case SWITZERLAND:
                currency = new SWIcurrency();
                break;
            case UNITED_KINGDOM:
                currency = new UKcurrency();
                break;
            case AUSTRALIA:
                currency = new ASTcurrency();
                break;
            case SOUTH_AFRICA:
                currency = new SOUTHAFRICAcurrency();
                break;
            default:
                currency = new USAcurrency();
                break;
        }
        return currency;
    }
}
