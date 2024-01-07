from django.core.management.base import BaseCommand, CommandError

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'Get all users in the config'

    def add_arguments(self, parser):
        parser.add_argument('--u', dest='u', help='find a user', type=str)

    def handle(self, *args, **options):
        if options['u']:
            try:
                user = CustomUser.objects.get(username=options['u'])
                self.stdout.write(f'{user.id}. Username:{user.username}\n Email:{user.email}')
            except CustomUser.DoesNotExist:
                raise CommandError(f'%s does not exists' % options['u'])
        else:
            users = CustomUser.objects.all().order_by('-id')
            for user in users:
                self.stdout.write(f'{user.id}. Username:{user.username}\n Email:{user.email}')
