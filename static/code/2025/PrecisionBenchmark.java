package org.sample;

import org.apfloat.Apfloat;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.math.BigDecimal;
import java.math.MathContext;
import java.util.concurrent.TimeUnit;



@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(value = 2)
@Warmup(iterations = 2, time = 1)
@Measurement(iterations = 2, time = 3)
public class PrecisionBenchmark {

    private static final int ITERATIONS = 100;

    @State(Scope.Thread)
    public static class BenchmarkState {
        BigDecimal aBD;
        BigDecimal bBD;
        Apfloat aAF;
        Apfloat bAF;
        MathContext mc;

        @Param({"25", "27", "30", "500", "1000"})  // Add different precision levels here
        int precision;

        @Setup(Level.Trial)
        public void setUp() {
            mc = new MathContext(precision);
            aBD = new BigDecimal("12345.6789012345678901234567890123456789", mc);
            bBD = new BigDecimal("98765.4321098765432109876543210987654321", mc);
            aAF = new Apfloat("12345.6789012345678901234567890123456789", precision);
            bAF = new Apfloat("98765.4321098765432109876543210987654321", precision);
        }
    }

    @Benchmark
    public void testBigDecimalAddition(BenchmarkState state, Blackhole bh) {
        for (int i = 0; i < ITERATIONS; i++) {
            BigDecimal result = state.aBD.add(state.bBD);
            bh.consume(result);
        }
    }

    @Benchmark
    public void testApFloatAddition(BenchmarkState state, Blackhole bh) {
        for (int i = 0; i < ITERATIONS; i++) {
            Apfloat result = state.aAF.add(state.bAF);
            bh.consume(result);
        }
    }

    @Benchmark
    public void testBigDecimalMultiplication(BenchmarkState state, Blackhole bh) {
        for (int i = 0; i < ITERATIONS; i++) {
            BigDecimal result = state.aBD.multiply(state.bBD);
            bh.consume(result);
        }
    }

    @Benchmark
    public void testApFloatMultiplication(BenchmarkState state, Blackhole bh) {
        for (int i = 0; i < ITERATIONS; i++) {
            Apfloat result = state.aAF.multiply(state.bAF);
            bh.consume(result);
        }
    }

    @Benchmark
    public void testBigDecimalDivision(BenchmarkState state, Blackhole bh) {
        for (int i = 0; i < ITERATIONS; i++) {
            BigDecimal result = state.aBD.divide(state.bBD, state.mc);
            bh.consume(result);
        }
    }

    @Benchmark
    public void testApFloatDivision(BenchmarkState state, Blackhole bh) {
        for (int i = 0; i < ITERATIONS; i++) {
            Apfloat result = state.aAF.divide(state.bAF);
            bh.consume(result);
        }
    }

}

