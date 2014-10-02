# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import entropy.base


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.agent_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Commitment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occured_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DecrementCommitmentLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('receiving_agent', models.ForeignKey(related_name=b'rea_decrementcommitmentline_reveiving_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occured_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DecrementEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Event')),
                ('quantity', models.FloatField()),
                ('receiving_agent', models.ForeignKey(related_name=b'rea_decrementevent_reveiving_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event', models.Model),
        ),
        migrations.CreateModel(
            name='IncrementCommitmentLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('providing_agent', models.ForeignKey(related_name=b'rea_incrementcommitmentline_providing_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncrementEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Event')),
                ('quantity', models.FloatField()),
                ('providing_agent', models.ForeignKey(related_name=b'rea_incrementevent_providing_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event', models.Model),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.resource_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('contract_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Contract')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.contract',),
        ),
        migrations.AddField(
            model_name='incrementevent',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incrementcommitmentline',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='commitment',
            field=models.ForeignKey(related_name=b'rea_event_commitment', to='rea.Commitment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name=b'polymorphic_rea.event_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementevent',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementcommitmentline',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name=b'polymorphic_rea.contract_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='providing_agent',
            field=models.ForeignKey(related_name=b'rea_contract_providing_agent', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='receiving_agent',
            field=models.ForeignKey(related_name=b'rea_contract_receiving_agent', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='contract',
            field=models.ForeignKey(to='rea.Contract'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='decrement_line',
            field=models.ForeignKey(related_name=b'rea_commitment_decrement_commitment_lines', to='rea.DecrementCommitmentLine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='increment_line',
            field=models.ForeignKey(related_name=b'rea_commitment_increment_commitment_lines', to='rea.IncrementCommitmentLine'),
            preserve_default=True,
        ),
    ]
