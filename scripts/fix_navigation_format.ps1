# Script para actualizar el formato de navegación en todos los notebooks
# Autor: Sistema automatizado
# Fecha: 2025-12-13

$notebooks = @(
    "notebooks\10_data_engineering\DE-01-ingesta.ipynb",
    "notebooks\10_data_engineering\DE-02-pipeline_incremental.ipynb",
    "notebooks\10_data_engineering\DE-03-etl_basico.ipynb",
    "notebooks\10_data_engineering\DE-04-kafka_streaming.ipynb",
    "notebooks\20_data_architecture\DA-01-modelo_dimensional.ipynb",
    "notebooks\20_data_architecture\DA-02-data_lake_partitions.ipynb",
    "notebooks\30_data_science_ml\DS-01-eda.ipynb",
    "notebooks\30_data_science_ml\DS-02-estacionalidad.ipynb",
    "notebooks\30_data_science_ml\DS-03-service_level_cost_tradeoff.ipynb",
    "notebooks\30_data_science_ml\DS-04-last_mile_analytics.ipynb",
    "notebooks\30_data_science_ml\DS-05-supply_risk_scenarios.ipynb",
    "notebooks\30_data_science_ml\DS-06-forecast_arima.ipynb",
    "notebooks\30_data_science_ml\DS-07-supplier_risk_ml.ipynb",
    "notebooks\40_business_analytics_bi\BA-01-dashboard_otif.ipynb",
    "notebooks\40_business_analytics_bi\BA-02-cost_to_serve.ipynb",
    "notebooks\40_business_analytics_bi\BA-02-sop_scenarios.ipynb",
    "notebooks\40_business_analytics_bi\BA-03-warehouse_productivity.ipynb",
    "notebooks\40_business_analytics_bi\BA-04-supplier_performance.ipynb",
    "notebooks\40_business_analytics_bi\BA-05-dashboard_ejecutivo.ipynb",
    "notebooks\50_optimization_or\OR-01-stock_seguridad.ipynb",
    "notebooks\50_optimization_or\OR-02-politicas_inventario.ipynb",
    "notebooks\50_optimization_or\OR-02-vrp_capacidad.ipynb",
    "notebooks\50_optimization_or\OR-03-capacity_planning_dc_fleet.ipynb",
    "notebooks\50_optimization_or\OR-04-multi_echelon_inventory.ipynb",
    "notebooks\50_optimization_or\OR-05-warehouse_slotting.ipynb",
    "notebooks\50_optimization_or\OR-06-dock_queue_simulation.ipynb",
    "notebooks\50_optimization_or\OR-07-safety_stock_intro.ipynb",
    "notebooks\50_optimization_or\OR-08-production_scheduling.ipynb",
    "notebooks\50_optimization_or\OR-09-network_optimization.ipynb",
    "notebooks\60_realtime_iot\RT-01-stream_tracking.ipynb",
    "notebooks\60_realtime_iot\RT-02-fleet_predictive_maintenance.ipynb",
    "notebooks\60_realtime_iot\RT-03-cold_chain_monitoring.ipynb",
    "notebooks\60_realtime_iot\RT-04-iot_sensors_intro.ipynb",
    "notebooks\60_realtime_iot\TR-01-transporte_masivo.ipynb",
    "notebooks\70_ai_gen_agents\GEN-01-rag_kpi.ipynb",
    "notebooks\70_ai_gen_agents\GEN-02-llm_text_analysis.ipynb",
    "notebooks\80_governance_quality\DG-01-perfilado_calidad.ipynb",
    "notebooks\90_capstone_end2end\CAP-01-torre_control.ipynb"
)

$updated = 0
$errors = 0

foreach ($notebook in $notebooks) {
    try {
        Write-Host "Procesando: $notebook" -ForegroundColor Cyan
        
        $content = Get-Content $notebook -Raw -Encoding UTF8
        
        # Reemplazar el formato antiguo por el nuevo
        $oldPattern = '## 📚 Navegación'
        $newPattern = '🧩 Navegación'
        
        if ($content -match [regex]::Escape($oldPattern)) {
            # Reemplazar ## 📚 por 🧩
            $content = $content -replace '## 📚 Navegación', '🧩 Navegación'
            
            # Remover ** de los enlaces de anterior y siguiente
            $content = $content -replace '\*\*← Anterior:\*\* ', '← Anterior: '
            $content = $content -replace '\*\*Siguiente →:\*\* ', 'Siguiente →: '
            
            # Reemplazar 📑 por 📋 y remover **
            $content = $content -replace '\*\*📑 Recursos:\*\*', '📋 Recursos:'
            
            # Guardar cambios
            $content | Set-Content $notebook -Encoding UTF8 -NoNewline
            
            Write-Host "  ✓ Actualizado correctamente" -ForegroundColor Green
            $updated++
        } else {
            Write-Host "  - No se encontró patrón de navegación" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  ✗ Error: $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Resumen de actualización:" -ForegroundColor Cyan
Write-Host "  Notebooks actualizados: $updated" -ForegroundColor Green
Write-Host "  Errores: $errors" -ForegroundColor $(if ($errors -eq 0) { 'Green' } else { 'Red' })
Write-Host "========================================`n" -ForegroundColor Cyan
