#!/usr/bin/env python
import os
import sys


def main(execute):
    execute(sys.argv)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimpleAppointmentWebApp.settings")

    from django.core.management import execute_from_command_line
    
    print (" args-> ".join(sys.argv))
    
    main(execute_from_command_line)


