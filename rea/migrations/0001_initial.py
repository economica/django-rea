# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import entropy.base
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='REAObject',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, blank=True, max_length=32, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('reaobject_ptr', models.OneToOneField(to='rea.REAObject', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
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
                ('event_ptr', models.OneToOneField(to='rea.Event', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
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
                ('event_ptr', models.OneToOneField(to='rea.Event', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event',),
        ),
        migrations.CreateModel(
            name='IncrementCommitment',
            fields=[
                ('commitment_ptr', models.OneToOneField(to='rea.Commitment', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
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
                ('commitment_ptr', models.OneToOneField(to='rea.Commitment', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
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
                ('event_ptr', models.OneToOneField(to='rea.Event', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
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
                ('reaobject_ptr', models.OneToOneField(to='rea.REAObject', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject', entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('reaobject_ptr', models.OneToOneField(to='rea.REAObject', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject',),
        ),
        migrations.CreateModel(
            name='Reconciliation',
            fields=[
                ('reaobject_ptr', models.OneToOneField(to='rea.REAObject', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('value', models.FloatField()),
                ('unbalanced_value', models.FloatField()),
                ('is_reconciled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject',),
        ),
        migrations.CreateModel(
            name='ReconciliationInitiator',
            fields=[
                ('reconciliation_ptr', models.OneToOneField(to='rea.Reconciliation', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reconciliation',),
        ),
        migrations.CreateModel(
            name='ReconciliationTerminator',
            fields=[
                ('reconciliation_ptr', models.OneToOneField(to='rea.Reconciliation', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('initiator', models.ForeignKey(to='rea.ReconciliationInitiator', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reconciliation',),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('reaobject_ptr', models.OneToOneField(to='rea.REAObject', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject', entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('contract_ptr', models.OneToOneField(to='rea.Contract', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.contract',),
        ),
        migrations.AddField(
            model_name='reconciliationinitiator',
            name='terminator',
            field=models.ForeignKey(to='rea.ReconciliationTerminator', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reconciliation',
            name='event',
            field=models.ForeignKey(to='rea.Event', related_name='rea_reconciliation_event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reconciliation',
            name='events',
            field=models.ManyToManyField(to='rea.Event', related_name='rea_reconciliation_events'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reaobject',
            name='polymorphic_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType', related_name='polymorphic_rea.reaobject_set', null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incrementevent',
            name='providing_agent',
            field=models.ForeignKey(to='rea.Agent', related_name='rea_incrementevent_providing_agents'),
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
            field=models.ForeignKey(to='rea.Agent', related_name='rea_incrementcommitment_providing_agents'),
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
            field=models.ForeignKey(to='rea.Agent', related_name='rea_decrementevent_reveiving_agents'),
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
            field=models.ForeignKey(to='rea.Agent', related_name='rea_decrementcommitment_reveiving_agents'),
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
            name='providing_agent',
            field=models.ForeignKey(to='rea.Agent', related_name='rea_contract_providing_agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='receiving_agent',
            field=models.ForeignKey(to='rea.Agent', related_name='rea_contract_receiving_agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='contract',
            field=models.ForeignKey(to='rea.Contract'),
            preserve_default=True,
        ),
    ]
