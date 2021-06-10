from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from ads_bot.bot import bot
        bot.run()
