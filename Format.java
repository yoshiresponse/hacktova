// Example for a Java function that is called by a MapForce mapping
// If you make changes to this file, recompile with: javac Format.java

package Format;

public class Format
{
    public static String FormatNumber(java.math.BigDecimal n)
    {
        java.text.NumberFormat formatter = new java.text.DecimalFormat("#,##0.00");
        return formatter.format(n.doubleValue());
    }
}
