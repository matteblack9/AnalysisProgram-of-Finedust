package alfio.util;

import java.math.BigDecimal;
import java.util.function.Function;

import static java.math.RoundingMode.HALF_DOWN;
import static java.math.RoundingMode.HALF_UP;
import static java.math.RoundingMode.UP;

public interface Currency {

    public static final BigDecimal HUNDRED = new BigDecimal("100.00");

    public int addVAT(int priceInCents, BigDecimal vat);
    public BigDecimal addVAT(BigDecimal price, BigDecimal vat);
    public int extractVAT(int priceInCents, BigDecimal vat);
    //ADD_BY_KHW


    public BigDecimal extractVAT(BigDecimal price, BigDecimal vat);
    public int calcPercentage(int priceInCents, BigDecimal vat);
    public <T extends Number> T calcPercentage(long priceInCents, BigDecimal vat, Function<BigDecimal, T> converter);
    public BigDecimal calcVat(BigDecimal price, BigDecimal percentage);

    public BigDecimal centsToCur(int cents);
    public BigDecimal centsToCur(long cents);
    public double unitToCur(BigDecimal unit);
    public  <T extends Number> T unitToCur(BigDecimal unit, Function<BigDecimal, T> converter);
    public String formatCur(long cents);
    public String formatCur(int cents);
}
