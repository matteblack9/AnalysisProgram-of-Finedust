package alfio.util;

import java.math.BigDecimal;
import java.util.function.Function;

import static alfio.util.MonetaryUtil.centsToUnit;
import static java.math.RoundingMode.HALF_UP;

public class USAcurrency implements Currency {
    USAcurrency() {}

    float exchangeRate = 1;

    public static final BigDecimal HUNDRED = new BigDecimal("100.00");

    public BigDecimal centsToCur(int cents) {
        return new BigDecimal(cents).divide(HUNDRED, 2, HALF_UP);
    }
    public BigDecimal centsToCur(long cents) {
        return new BigDecimal(cents).divide(HUNDRED, 2, HALF_UP);
    }

    public double unitToCur(BigDecimal unit) {
        return unitToCur(unit, BigDecimal::intValueExact);
    }

    public <T extends Number> T unitToCur(BigDecimal unit, Function<BigDecimal, T> converter) {
        BigDecimal result = unit.multiply(HUNDRED).setScale(0, HALF_UP);
        return converter.apply(result);
    }

    public String formatCur(long cents) {
        return centsToUnit(cents).toPlainString();
    }
    public String formatCur(int cents) {
        return centsToUnit(cents).toPlainString();
    }
}

