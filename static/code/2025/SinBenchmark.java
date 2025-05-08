@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Fork(value = 1)
@Warmup(iterations = 1, time = 1)
@Measurement(iterations = 3, time = 5)
public abstract class BaseBenchmark {

  @State(Scope.Thread)
  public static class BenchmarkState {
    MathContext mc;
    BigDecimal aBD, bBD;
    Apfloat aAF, bAF;

    @Param({ "25", "50", "500", "1000" }) // Add different precision levels here
    int precision;

    @Setup(Level.Trial)
    public void setUp() {
      mc = new MathContext(precision);
      aBD = new BigDecimal("12345.678901234567890123456789012345678934343434343434343434343434343434", mc);
      aAF = new Apfloat("12345.678901234567890123456789012345678934343434343434343434343434343434", precision);
    }
  }
}

public class Sin extends BaseBenchmark {

  @Benchmark
  public void BigDecimalSin(BenchmarkState state, Blackhole bh) {
    var result = BigDecimalMath.sin(state.aBD, state.mc);
    bh.consume(result);
  }

  @Benchmark
  public void ApfloatSin(BenchmarkState state, Blackhole bh) {
    var result = ApfloatMath.sin(state.aAF);
    bh.consume(result);
  }
}
