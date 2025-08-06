import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1754437245768 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://fiap-5mlet-tc2-b3-raw/raw/"], "recurse": True}, transformation_ctx="AmazonS3_node1754437245768")

# Script generated for node Rename Field
RenameField_node1754438470761 = RenameField.apply(frame=AmazonS3_node1754437245768, old_name="asset", new_name="ativo", transformation_ctx="RenameField_node1754438470761")

# Script generated for node Rename Field
RenameField_node1754438491725 = RenameField.apply(frame=RenameField_node1754438470761, old_name="type", new_name="tipo", transformation_ctx="RenameField_node1754438491725")

# Script generated for node Rename Field
RenameField_node1754438552692 = RenameField.apply(frame=RenameField_node1754438491725, old_name="part", new_name="participacao", transformation_ctx="RenameField_node1754438552692")

# Script generated for node Rename Field
RenameField_node1754439050491 = RenameField.apply(frame=RenameField_node1754438552692, old_name="extraction_date", new_name="data_extracao", transformation_ctx="RenameField_node1754439050491")

# Script generated for node Rename Field
RenameField_node1754440310180 = RenameField.apply(frame=RenameField_node1754439050491, old_name="cod", new_name="codigo", transformation_ctx="RenameField_node1754440310180")

# Script generated for node Rename Field
RenameField_node1754440491046 = RenameField.apply(frame=RenameField_node1754440310180, old_name="segment", new_name="segmento", transformation_ctx="RenameField_node1754440491046")

# Script generated for node Rename Field
RenameField_node1754440552944 = RenameField.apply(frame=RenameField_node1754440491046, old_name="partacum", new_name="participacao_acumulada", transformation_ctx="RenameField_node1754440552944")

# Script generated for node Aggregate
Aggregate_node1754440608946 = sparkAggregate(glueContext, parentFrame = RenameField_node1754440552944, groups = ["data_extracao", "codigo"], aggs = [["theoricalqty", "sum"]], transformation_ctx = "Aggregate_node1754440608946")

# Script generated for node SQL Query
SqlQuery661 = '''
select 
data_extracao,
DATEDIFF(data_extracao, DATE_FORMAT(data_extracao, 'yyyy-01-01')) AS dias_desde_inicio_ano,
*
from myDataSource
'''
SQLQuery_node1754443396987 = sparkSqlQuery(glueContext, query = SqlQuery661, mapping = {"myDataSource":Aggregate_node1754440608946}, transformation_ctx = "SQLQuery_node1754443396987")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1754443396987, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1754439934465", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1754443418089 = glueContext.write_dynamic_frame.from_options(frame=SQLQuery_node1754443396987, connection_type="s3", format="glueparquet", connection_options={"path": "s3://fiap-5mlet-tc2-b3-refined", "partitionKeys": ["data_extracao", "codigo"]}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1754443418089")

job.commit()