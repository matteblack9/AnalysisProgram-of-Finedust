package alfio.util;

import java.math.BigDecimal;
import java.util.function.Function;

import static java.math.RoundingMode.HALF_UP;

public class SWIcurrency implements Currency {

    double exchangeRate = 0.98501;

    public static final BigDecimal HUNDRED = new BigDecimal("100.00");

    public BigDecimal centsToCur(int cents) {
        return new BigDecimal(exchangeRate).multiply(new BigDecimal(cents).divide(HUNDRED, 2, HALF_UP));
    }
    public BigDecimal centsToCur(long cents) {
        return new BigDecimal(exchangeRate).multiply(new BigDecimal(cents).divide(HUNDRED, 2, HALF_UP));
    }

    public double unitToCur(BigDecimal unit) {
        return exchangeRate * (double)unitToCur(unit, BigDecimal::intValueExact);
    }

    public <T extends Number> T unitToCur(BigDecimal unit, Function<BigDecimal, T> converter) {
        BigDecimal result = unit.multiply(HUNDRED).setScale(0, HALF_UP);
        return converter.apply(result);
    }

    public String formatCur(long cents) {
        return new BigDecimal(exchangeRate).multiply(centsToCur(cents)).toPlainString();
    }

    public String formatCur(int cents) {
        return new BigDecimal(exchangeRate).multiply(centsToCur(cents)).toPlainString();
    }
}
