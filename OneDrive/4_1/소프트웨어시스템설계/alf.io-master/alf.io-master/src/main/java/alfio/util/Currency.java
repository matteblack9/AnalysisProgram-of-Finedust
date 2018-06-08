package alfio.util;

import java.math.BigDecimal;
import java.util.function.Function;

import static java.math.RoundingMode.HALF_UP;

public interface Currency {
    public BigDecimal centsToCur(int cents);
    public BigDecimal centsToCur(long cents);
    public double unitToCur(BigDecimal unit);
    public  <T extends Number> T unitToCur(BigDecimal unit, Function<BigDecimal, T> converter);
    public String formatCur(long cents);
    public String formatCur(int cents);
}
