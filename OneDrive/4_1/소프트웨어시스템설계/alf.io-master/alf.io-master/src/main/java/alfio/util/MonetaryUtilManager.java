/**
 * This file is part of alf.io.
 *
 * alf.io is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * alf.io is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with alf.io.  If not, see <http://www.gnu.org/licenses/>.
 **/

//COMMENT BY KHW

package alfio.util;

import java.math.BigDecimal;
import java.util.function.Function;

import static alfio.util.MonetaryUtil.centsToUnit;
import static java.math.RoundingMode.*;

public abstract class MonetaryUtilManager {

    MonetaryUtilManager(){
    }

    //MonetaryUtil is a class that has functions like calculating prices or calculating VAT.
    //The cents scale expresses 100.00 to 10000 BECAREFUL!
    //The scale of VAT is dollar(unit)
    //The scale of parameter 'price' is cent.

    public static final BigDecimal HUNDRED = new BigDecimal("100.00");
    choosingCurrencyFactory currentfactory = new choosingCurrencyFactory();
    Currency currency = null;

    //VAT is Value Added Tax

    public static int addVAT(int priceInCents, BigDecimal vat) {
        return addVAT(new BigDecimal(priceInCents), vat).intValueExact();
    }
    //Add the VAT for the price ,and change the type from BigDecimal to integer.

    public static BigDecimal addVAT(BigDecimal price, BigDecimal vat) {
        return price.add(price.multiply(vat.divide(HUNDRED, 5, UP))).setScale(0, HALF_UP);
    }

    //the parameter vat does not means price but percent.
    //If you put the parameter to this function, let me show the example of use.
    //Here is the value of parameter, price = 8000 vat = 2.5.
    //then this function implements the process that
    //" 8000 + 8000 * (2.5 / 100) = 8250

    //
    public static int extractVAT(int priceInCents, BigDecimal vat) {
        return extractVAT(new BigDecimal(priceInCents), vat).intValueExact();
    }
    //ADD_BY_KHW


    public static BigDecimal extractVAT(BigDecimal price, BigDecimal vat) {
        return price.subtract(price.divide(BigDecimal.ONE.add(vat.divide(HUNDRED, 5, UP)), 5, HALF_DOWN));
    }
    //This parameter 'price' of this function is the price included VAT.
    //Let's assume the value of parameter 'price' is 10750.
    //and the value of 'vat' is 7.5
    //the this function returns the value 750 cents. so the origin price of the parameter 'price' is 10750 - 750.


    public static int calcPercentage(int priceInCents, BigDecimal vat) {
        return calcPercentage((long) priceInCents, vat, BigDecimal::intValueExact);
    }

    public static <T extends Number> T calcPercentage(long priceInCents, BigDecimal vat, Function<BigDecimal, T> converter) {
        BigDecimal result = new BigDecimal(priceInCents).multiply(vat.divide(HUNDRED, 5, UP))
            .setScale(0, HALF_UP);
        return converter.apply(result);
    }
    //This function calculates the VAT price from the origin price.
    //same function with 'calcPercentage', 'calcVat'
    //The role of 'Function<K, T> converter' proceeds as follows
    //if you put the value of K type 'converter' produces the same value of T type.

    public static BigDecimal calcVat(BigDecimal price, BigDecimal percentage) {
        return price.multiply(percentage.divide(HUNDRED, 5, HALF_UP));
    }


    public void requestCurrency(choosingCurrencyID country){
        this.currency = currentfactory.get(country);
    }

    public BigDecimal getcentsToCur(int cents) {
        return new BigDecimal(currency.formatCur(cents));
    }

    public BigDecimal getcentsToCur(long cents) {
        return new BigDecimal(currency.formatCur(cents));
    }

    public double getUnitToCur(BigDecimal unit){
        return currency.unitToCur(unit);
    }

    public <T extends Number> T getUnitToCur(BigDecimal unit, Function<BigDecimal, T> converter) {
        return currency.unitToCur(unit, converter);
    }

    public String getformatCur(long cents) {
        return currency.formatCur(cents);
    }
    public String getformatCur(int cents) {
        return currency.formatCur(cents);
    }
}
