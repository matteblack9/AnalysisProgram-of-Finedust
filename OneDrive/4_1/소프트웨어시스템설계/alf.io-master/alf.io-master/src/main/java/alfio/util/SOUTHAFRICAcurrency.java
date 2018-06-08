package alfio.util;

import java.math.BigDecimal;
import java.util.function.Function;

import static java.math.RoundingMode.HALF_DOWN;
import static java.math.RoundingMode.HALF_UP;
import static java.math.RoundingMode.UP;

public class SOUTHAFRICAcurrency implements Currency {
    double exchangeRate = 13.0445;

    public static final BigDecimal HUNDRED = new BigDecimal("100.00");

    public int addVAT(int priceInCents, BigDecimal vat) {
        return addVAT(new BigDecimal(priceInCents), vat).intValueExact();
    }
    //Add the VAT for the price ,and change the type from BigDecimal to integer.

    public BigDecimal addVAT(BigDecimal price, BigDecimal vat) {
        return price.add(price.multiply(vat.divide(HUNDRED, 5, UP))).setScale(0, HALF_UP);
    }

    public int extractVAT(int priceInCents, BigDecimal vat) {
        return extractVAT(new BigDecimal(priceInCents), vat).intValueExact();
    }
    //ADD_BY_KHW


    public BigDecimal extractVAT(BigDecimal price, BigDecimal vat) {
        return price.subtract(price.divide(BigDecimal.ONE.add(vat.divide(HUNDRED, 5, UP)), 5, HALF_DOWN));
    }

    public int calcPercentage(int priceInCents, BigDecimal vat) {
        return calcPercentage((long) priceInCents, vat, BigDecimal::intValueExact);
    }

    public <T extends Number> T calcPercentage(long priceInCents, BigDecimal vat, Function<BigDecimal, T> converter) {
        BigDecimal result = new BigDecimal(priceInCents).multiply(vat.divide(HUNDRED, 5, UP))
            .setScale(0, HALF_UP);
        return converter.apply(result);
    }

    public BigDecimal calcVat(BigDecimal price, BigDecimal percentage) {
        return price.multiply(percentage.divide(HUNDRED, 5, HALF_UP));
    }

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
