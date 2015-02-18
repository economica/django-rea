# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields
import entropy.base


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='REAObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('reaobject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.REAObject')),
                ('occured_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject',),
        ),
        migrations.CreateModel(
            name='IncrementEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Event')),
                ('quantity', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event', models.Model),
        ),
        migrations.CreateModel(
            name='Commitment',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event',),
        ),
        migrations.CreateModel(
            name='IncrementCommitment',
            fields=[
                ('commitment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Commitment')),
                ('quantity', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.commitment', models.Model),
        ),
        migrations.CreateModel(
            name='DecrementCommitment',
            fields=[
                ('commitment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Commitment')),
                ('quantity', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.commitment', models.Model),
        ),
        migrations.CreateModel(
            name='DecrementEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Event')),
                ('quantity', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event', models.Model),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('reaobject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.REAObject')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject',),
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('reaobject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.REAObject')),
                ('name', models.CharField(max_length=1024)),
                ('name_plural', models.CharField(max_length=1024, blank=True)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject', entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Reconciliation',
            fields=[
                ('reaobject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.REAObject')),
                ('value', models.FloatField()),
                ('unbalanced_value', models.FloatField()),
                ('marked_reconciled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject',),
        ),
        migrations.CreateModel(
            name='ReconciliationInitiator',
            fields=[
                ('reconciliation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Reconciliation')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reconciliation',),
        ),
        migrations.CreateModel(
            name='ReconciliationTerminator',
            fields=[
                ('reconciliation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Reconciliation')),
                ('initiators', models.ManyToManyField(related_name='terminators', null=True, to='rea.ReconciliationInitiator')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reconciliation',),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('reaobject_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.REAObject')),
                ('name', models.CharField(max_length=1024)),
                ('name_plural', models.CharField(max_length=1024, blank=True)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject', entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ItemizedResource',
            fields=[
                ('resource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Resource')),
                ('serial', models.CharField(unique=True, max_length=1024)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.resource',),
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('contract_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Contract')),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.contract', entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.AddField(
            model_name='reconciliation',
            name='event',
            field=models.ForeignKey(related_name='rea_reconciliation_event', to='rea.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reconciliation',
            name='events',
            field=models.ManyToManyField(related_name='rea_reconciliation_events', to='rea.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reaobject',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_rea.reaobject_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incrementevent',
            name='providing_agent',
            field=models.ForeignKey(related_name='rea_incrementevent_providing_agents', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incrementevent',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incrementcommitment',
            name='providing_agent',
            field=models.ForeignKey(related_name='rea_incrementcommitment_providing_agents', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incrementcommitment',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementevent',
            name='receiving_agent',
            field=models.ForeignKey(related_name='rea_decrementevent_reveiving_agents', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementevent',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementcommitment',
            name='receiving_agent',
            field=models.ForeignKey(related_name='rea_decrementcommitment_reveiving_agents', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementcommitment',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='provider',
            field=models.ForeignKey(related_name='rea_contract_providers', default=1, to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='recipient',
            field=models.ForeignKey(related_name='rea_contract_recipients', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='contract',
            field=models.ForeignKey(to='rea.Contract'),
            preserve_default=True,
        ),
    ]
