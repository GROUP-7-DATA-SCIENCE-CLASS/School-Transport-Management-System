
from services.transport_service import TransportService


def main():
    """Application entry point."""

    transport_system = TransportService(
        school_name="Sunrise Junior School"
    )

    print("=" * 50)
    print(f"  {transport_system.school_name}")
    print("  SCHOOL TRANSPORT MANAGEMENT SYSTEM")
    print("=" * 50)

    print("\nApplication initialized successfully.")
    print("Transport service is ready.")


if __name__ == "__main__":
    main()
