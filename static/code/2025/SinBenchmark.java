@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(value = 1)
@Warmup(iterations = 2, time = 2)
@Measurement(iterations = 2, time = 2)
public abstract class BaseBenchmark {

  protected static final int ITERATIONS = 200;

  @State(Scope.Thread)
  public static class BenchmarkState {
    MathContext mc;
    BigDecimal aBD;
    Apfloat aAF;

    @Param({ "25", "1000" }) // Add different precision levels here
    int precision;

    @Setup(Level.Trial)
    public void setUp() {
      mc = new MathContext(precision);
      aBD = new BigDecimal("12345.6789012345678901234567890123456789", mc);
      aBD = new Apfloat("12345.6789012345678901234567890123456789", precision);
    }
  }
}

public class Sin extends BaseBenchmark {

  @Benchmark
  public void testBigDecimalSin(BenchmarkState state, Blackhole bh) {
    for (int i = 0; i < ITERATIONS; i++) {
      var result = BigDecimalMath.sin(state.aBD, state.mc);
      bh.consume(result);
    }
  }

  @Benchmark
  public void testApfloatSin(BenchmarkState state, Blackhole bh) {
    for (int i = 0; i < ITERATIONS; i++) {
      var result = ApfloatMath.sin(state.aBD);
      bh.consume(result);
    }
  }

}
