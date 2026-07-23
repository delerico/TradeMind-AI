from app.backtest.engine import BacktestEngine
from app.collector.market_collector import MarketCollector
from app.database.database import Base, SessionLocal, engine
from app.database.market_repository import MarketDataRepository
from app.indicators.indicator_service import IndicatorService
from app.services.market_import_service import MarketImportService
from app.strategies.moving_average_cross import MovingAverageCrossStrategy


def main() -> None:
    """
    TradeMind AI entry point.
    """

    # Create database tables
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        collector = MarketCollector()
        repository = MarketDataRepository(session)

        # Import market data into the database
        import_service = MarketImportService(
            collector=collector,
            repository=repository,
        )

        imported = import_service.import_symbol(
            symbol="AAPL",
            period="6mo",
        )

        print(f"\nImported {imported} records.")

        # Download market data
        data = collector.get_stock(
            symbol="AAPL",
            period="6mo",
        )

        # Calculate indicators
        indicator_service = IndicatorService()
        data = indicator_service.add_basic_indicators(data)

        # Create strategy
        strategy = MovingAverageCrossStrategy()

        # Run backtest
        backtest_engine = BacktestEngine(
            initial_capital=10_000,
        )

        result = backtest_engine.run(
            strategy=strategy,
            data=data,
            symbol="AAPL",
        )

        print()
        print("=" * 80)
        print("BACKTEST RESULTS")
        print("=" * 80)

        print(f"Initial Capital : ${result.initial_capital:,.2f}")
        print(f"Final Capital   : ${result.final_capital:,.2f}")
        print(f"Total Return    : {result.total_return:.2f}%")
        print(f"Trades          : {result.total_trades}")
        print(f"Winning Trades  : {result.winning_trades}")
        print(f"Losing Trades   : {result.losing_trades}")
        print(f"Win Rate        : {result.win_rate:.2f}%")

        print()
        print("=" * 80)
        print("TRADE HISTORY")
        print("=" * 80)

        if result.trades:
            for trade in result.trades:
                print(
                    f"{trade.entry_date.date()} -> {trade.exit_date.date()} | "
                    f"BUY ${trade.entry_price:.2f} | "
                    f"SELL ${trade.exit_price:.2f} | "
                    f"Profit ${trade.profit:.2f} "
                    f"({trade.return_pct:.2f}%)"
                )
        else:
            print("No trades generated.")

    finally:
        session.close()


if __name__ == "__main__":
    main()