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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('uuid', uuidfield.fields.UUIDField(max_length=32, unique=True, blank=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('reaobject_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.REAObject')),
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
                ('event_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Event')),
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
                ('event_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event',),
        ),
        migrations.CreateModel(
            name='IncrementCommitment',
            fields=[
                ('commitment_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Commitment')),
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
                ('commitment_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Commitment')),
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
                ('event_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Event')),
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
                ('reaobject_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.REAObject')),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
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
                ('reaobject_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.REAObject')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reaobject',),
        ),
        migrations.CreateModel(
            name='Reconciliation',
            fields=[
                ('reaobject_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.REAObject')),
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
                ('reconciliation_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Reconciliation')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reconciliation',),
        ),
        migrations.CreateModel(
            name='ReconciliationTerminator',
            fields=[
                ('reconciliation_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Reconciliation')),
                ('initiator', models.ForeignKey(null=True, to='rea.ReconciliationInitiator')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.reconciliation',),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('reaobject_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.REAObject')),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
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
                ('contract_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='rea.Contract')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.contract',),
        ),
        migrations.AddField(
            model_name='reconciliationinitiator',
            name='terminator',
            field=models.ForeignKey(null=True, to='rea.ReconciliationTerminator'),
            preserve_default=True,
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
            field=models.ForeignKey(editable=False, related_name='polymorphic_rea.reaobject_set', null=True, to='contenttypes.ContentType'),
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
            name='providing_agent',
            field=models.ForeignKey(related_name='rea_contract_providing_agent', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='receiving_agent',
            field=models.ForeignKey(related_name='rea_contract_receiving_agent', to='rea.Agent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='contract',
            field=models.ForeignKey(to='rea.Contract'),
            preserve_default=True,
        ),
    ]
